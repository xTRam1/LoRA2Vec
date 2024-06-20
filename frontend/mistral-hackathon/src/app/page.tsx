"use client";

// import bio from "@/assets/bio.jpg";
// import physics from "@/assets/physics.jpeg";
import { useEffect, useState } from "react";
import { BiAtom } from "react-icons/bi";
import { MdHealthAndSafety } from "react-icons/md";
import { PiDna } from "react-icons/pi";
import { SlChemistry } from "react-icons/sl";
import styles from "./page.module.css";

interface Message {
  id: number;
  text: string; // assuming `text` is a string; adjust the type as necessary
  sender: string;
}

const ChatbotUI = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState("");
  const [label, setLabel] = useState("");

  useEffect(() => {
    // Cleanup logic for messages if needed
  }, []);

  const handleUserInput = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const newMessage = {
      id: messages.length + 1,
      text: userInput,
      sender: "user",
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    const classifyResponse = await fetch("http://localhost:8000/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: userInput }),
    });
    const { label } = await classifyResponse.json();
    setLabel(label);

    const data = { label, query: userInput };
    streamResponse(data);
    setUserInput("");
  };

  const streamResponse = async (data) => {
    const url = "http://localhost:8000/generate";
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let buffer = "";

        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: prevMessages.length + 1,
            text: buffer,
            sender: "bot",
          },
        ]);

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          const lines = buffer.split("\n");
          buffer = lines.pop();

          lines.forEach((line) => {
            if (line.trim() !== "" && line.startsWith("data: ")) {
              const token = line.substring(5);
              if (token === '{"done": true}') {
                reader.cancel();
                return;
              }
              // Update the content of the single bot message
              setMessages((prevMessages) => {
                const updatedMessages = [...prevMessages];
                const botMessageIndex = updatedMessages.findLastIndex(
                  (m) => m.sender === "bot"
                );
                // Prevent duplication: only append if different from current text
                if (!updatedMessages[botMessageIndex].text.endsWith(token)) {
                  updatedMessages[botMessageIndex].text += token;
                }
                return updatedMessages;
              });
            }
          });
        }
      } else {
        console.error("Failed to fetch data", response.status);
      }
    } catch (error) {
      console.error("Error fetching data", error);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "row", width: "100%" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "left",
          alignItems: "center",
          flexDirection: "column",
          margin: "auto",
        }}
      >
        <SlChemistry
          className={styles.loraLogo}
          color={label == "Chemistry" ? "orange" : "grey"}
        />
        <BiAtom
          className={styles.loraLogo}
          color={label == "Physics" ? "blue" : "grey"}
        />
        <PiDna
          className={styles.loraLogo}
          color={label == "Biology" ? "green" : "grey"}
        />
        <MdHealthAndSafety
          className={styles.loraLogo}
          color={label == "Medical" ? "red" : "grey"}
        />
      </div>

      <div
        className="chatbot-container"
        style={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          height: "100vh",
        }}
      >
        <div
          className={styles.messagesList}
          style={{
            overflow: "auto",
            flexGrow: 1,
            marginTop: "8vh",
            fontSize: "1.5em",
          }}
        >
          {messages.map((message) => (
            <span
              key={message.id}
              className={
                message.sender == "bot" ? styles.messageBot : styles.messageUser
              }
              style={{ columnSpan: "all" }}
            >
              {message.text}
            </span>
          ))}
        </div>
        <form
          onSubmit={handleSubmit}
          className={styles.inputForm}
          style={{ display: "flex", padding: "10px" }}
        >
          <input
            type="text"
            className={styles.textInput}
            value={userInput}
            onChange={handleUserInput}
            placeholder="Type your message ..."
            style={{ flexGrow: 1 }}
          />
          <button type="submit" className={styles.sendButton}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatbotUI;
