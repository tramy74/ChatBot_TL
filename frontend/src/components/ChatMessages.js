import React, { useRef, useEffect } from "react";

const ChatMessages = ({ conversations }) => {
  const conversationEndRef = useRef(null);

  useEffect(() => {
    // Automatically scroll to the latest message
    conversationEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversations]);

  return (
    <div className="w-full max-w-5xl px-4">
      {conversations.map((conv, index) => (
        <div key={index} className="space-y-2">
          {/* User's Question */}
          <div className="flex justify-end">
            <div className="bg-blue-500 text-white px-4 py-2 rounded-lg max-w-md">
              {conv.question}
            </div>
          </div>
          {/* Bot's Answer */}
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-900 px-4 py-2 rounded-lg max-w-md text-left">
              {conv.answer}
            </div>
          </div>
        </div>
      ))}
      <div ref={conversationEndRef} />
    </div>
  );
};

export default ChatMessages;
