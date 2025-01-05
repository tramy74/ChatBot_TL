import React, { useState, useEffect } from "react";
import "./App.css";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";

function App() {
  const MAX_QUESTION_LENGTH = 200; // Set your maximum length here
  const [question, setQuestion] = useState("");
  const [conversations, setConversations] = useState([]);
  const [chatSessions, setChatSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const storedSessions = JSON.parse(localStorage.getItem("chatSessions")) || [];
    setChatSessions(storedSessions);
  
    if (storedSessions.length > 0) {
      const lastSession = storedSessions[storedSessions.length - 1];
      setCurrentSession(lastSession);
      setConversations(lastSession.messages);
    }
  }, []);
  
  useEffect(() => {
    localStorage.setItem("chatSessions", JSON.stringify(chatSessions));
  }, [chatSessions]);
  

  const handleSubmit = async (question, files) => {
    if (!question || !question.trim()) return;

    const formData = new FormData();
    formData.append("question", question);
    files.forEach((file) => {
        formData.append("files", file); // Send each file
    });

    try {
        const response = await fetch("http://localhost:8000/query", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        const { question: firstQuestion, answer, files: fileInfoList } = data;

        const newConversations = [
            ...conversations,
            { question: firstQuestion, answer, files: fileInfoList },
        ];
        setConversations(newConversations);

        if (!currentSession) {
            const newSession = {
                id: Date.now(),
                name: firstQuestion,
                messages: newConversations,
            };
            setChatSessions((prev) => [...prev, newSession]);
            setCurrentSession(newSession);
        } else {
            const updatedSessions = chatSessions.map((session) =>
                session.id === currentSession.id
                    ? { ...session, messages: newConversations }
                    : session
            );
            setChatSessions(updatedSessions);
        }
    } catch (error) {
        console.error("Error:", error);
    }
};
  
  const handleNewChat = () => {
    setConversations([]);
    setCurrentSession(null);
    setQuestion("");
  };

  const handleSelectSession = (session) => {
    setCurrentSession(session);
    setConversations(session.messages);
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar
        chatSessions={chatSessions}
        currentSession={currentSession}
        onNewChat={handleNewChat}
        onSelectSession={handleSelectSession}
      />
      <div className="flex flex-col flex-1">
        {errorMessage && (
          <div className="bg-red-100 text-red-700 p-2 text-center">
            {errorMessage}
          </div>
        )}
        <ChatWindow
          currentSession={currentSession}
          conversations={conversations}
          question={question} // Current question state
          setQuestion={setQuestion} // Pass setQuestion to update question
          handleSubmit={handleSubmit}
        />
      </div>
    </div>
  );
}

export default App;
