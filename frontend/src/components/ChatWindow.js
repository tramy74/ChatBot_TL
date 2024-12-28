import React, { useRef, useEffect, useState } from "react";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";

const ChatWindow = ({
  currentSession,
  conversations,
  question,
  setQuestion,
  handleSubmit,
  disableInput,
}) => {
  const hasConversations = conversations.length > 0;

  return (
    <div className="flex flex-col h-full w-full">
      {/* Title */}
      <h1 className="text-2xl font-bold p-4 text-center bg-white border-b border-gray-300 ">
        {currentSession ? currentSession.name : "Ask the Chatbot"}
      </h1>

      {/* Chat Messages */}
      <div
        className={`flex-1 overflow-y-auto ${
          !hasConversations && "flex items-center justify-center my-4"
        }`}
        style={{ maxHeight: "calc(100vh - 198px)" }} // Adjust the height dynamically
      >
        {hasConversations && <ChatMessages conversations={conversations} />}
      </div>

      {/* Chat Input */}
      <div
        className={`${
          hasConversations
            ? "bg-gray-100 border-gray-300 flex items-center justify-center mt-4 "
            : "flex items-center justify-center h-full px-4"
        }`}
      >
        <div className="w-full max-w-5xl px-4">
          <ChatInput
            question={question}
            onChange={setQuestion}
            onSubmit={handleSubmit}
            disableInput={disableInput}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
