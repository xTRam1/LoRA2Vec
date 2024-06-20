"use client";
import styles from './page.module.css';  // Adjust the path according to your project structure

// import { useState } from "react";

// const Home = () => {
//   const [query, setQuery] = useState("");
//   const [response, setResponse] = useState("");

//   const handleSubmit = async (e: { preventDefault: () => void; }) => {
//     e.preventDefault();
//     // Clear previous response
//     setResponse("");

//     const url = "http://localhost:8000/generate";
//     const headers = {
//       "Content-Type": "application/json",
//     };
//     const data = { query };

//     try {
//       const res = await fetch(url, {
//         method: "POST",
//         headers,
//         body: JSON.stringify(data),
//       });

//       if (res.ok) {
//         const reader = res.body.getReader();
//         const decoder = new TextDecoder("utf-8");
//         let buffer = "";

//         while (true) {
//           const { done, value } = await reader.read();
//           if (done) break;
//           buffer += decoder.decode(value, { stream: true });

//           const lines = buffer.split("\n");
//           buffer = lines.pop(); // Keep the last partial line in buffer

//           for (let line of lines) {
//             if (line.trim() !== "") {
//               if (line.startsWith("data: ")) {
//                 const token = line.substring(6);
//                 if (token === '{"done": true}') {
//                   reader.cancel();
//                   break;
//                 }
//                 setResponse((prevResponse) => prevResponse + token);
//               }
//             }
//           }
//         }
//       } else {
//         console.error("Failed to fetch data", res.status);
//       }
//     } catch (error) {
//       console.error("Error fetching data", error);
//     }
//   };

//   return (
//     <div>
//       <h1>Call FastAPI Endpoint with SSE</h1>
//       <form onSubmit={handleSubmit}>
//         <input
//           type="text"
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//           placeholder="Enter your query"
//         />
//         <button type="submit">Submit</button>
//       </form>
//       {response && (
//         <div style={{ overflow: "auto" }}>
//           <h2>Response:</h2>
//           <pre>{response}</pre>
//         </div>
//       )}
//     </div>
//   );
// };


import React, { useState } from 'react';

const ChatbotUI = () => {
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState("");

    const handleUserInput = event => {
        setUserInput(event.target.value);
    };

    const handleSubmit = event => {
        event.preventDefault();
        const newMessage = { id: messages.length + 1, text: userInput, sender: "user" };
        setMessages([...messages, newMessage]);
        sendToChatbot(userInput);
        setUserInput("");
    };

    const sendToChatbot = (input) => {
        // Simulate chatbot response
        setTimeout(() => {
            const botResponse = { id: messages.length + 2, text: `Echo: ${input}`, sender: "bot" };
            setMessages(messages => [...messages, botResponse]);
        }, 500);
    };

    return (
        <div className="chatbot-container">
            <div className={styles.messagesList}>
                {messages.map(message => (
                    <div key={message.id} className={`message ${message.sender}`}>
                        {message.text}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit}className={styles.inputForm}>
                <input 
                    type="text" 
                    className={styles.textInput}
                    value={userInput} 
                    onChange={handleUserInput} 
                    placeholder="Type your message ..." 
                />
                <button type="submit"
                        className={styles.sendButton}>Send</button>
            </form>
        </div>
    );
};

export default ChatbotUI;



