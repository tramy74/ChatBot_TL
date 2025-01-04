import React, { useRef, useEffect } from "react";

const ChatMessages = ({ conversations }) => {
  const conversationEndRef = useRef(null);

  useEffect(() => {
    conversationEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversations]);

  const renderFile = (file) => {
    return (
      <div className="flex items-center bg-gray-100 p-2 rounded-lg mt-2 shadow-md">
        {/* Biểu tượng file */}
        <div className="flex items-center justify-center w-10 h-10 rounded-full bg-pink-500 text-white mr-3">
          <i className="fas fa-file-alt"></i> {/* Font Awesome icon */}
        </div>
        {/* Tên file và loại file */}
        <div className="flex flex-col">
          <span className="font-medium text-gray-900">{file.filename}</span>
          <span className="text-sm text-gray-500">{file.type.toUpperCase()}</span>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col space-y-4 p-4">
      {conversations.map((conv, index) => (
        <div key={index} className="space-y-2">
          {/* Hiển thị file nếu có */}
          <div className="flex justify-end">
            <div >
            {conv.file && renderFile(conv.file)}
            </div>
          </div>
          

          {/* Hiển thị câu hỏi */}
          <div className="flex justify-end">
            <div className="bg-blue-500 text-white px-4 py-2 rounded-lg max-w-md">
              {conv.question}
            </div>
          </div>

          {/* Hiển thị câu trả lời */}
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
