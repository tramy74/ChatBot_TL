import React, { useRef, useEffect } from "react";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import ArrowUpwardRoundedIcon from "@mui/icons-material/ArrowUpwardRounded";
import Tooltip from "@mui/material/Tooltip";

export default function ChatInput({ question, onChange, onSubmit, disableInput }) {
  const textAreaRef = useRef(null);

  const handleSend = () => {
    if (onSubmit && !disableInput) {
      onSubmit(question); // Send the current question to the backend
      onChange(""); // Clear the input field after sending
    }
  };
  

  useEffect(() => {
    if (textAreaRef.current) {
      textAreaRef.current.style.height = "auto";
      textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`;
    }
  }, [question]);

  return (
    <div className="flex flex-col w-full bg-gray-200 rounded-xl py-3 ">
      <textarea
        ref={textAreaRef}
        placeholder="Nhập câu hỏi"
        value={question}
        onChange={(e) => onChange(e.target.value)}
        className="flex-grow bg-transparent bg-gray w-full border-none outline-none text-gray-700 placeholder-gray-500 resize-none overflow-y-auto max-h-32 px-4"
        rows={1}
        style={{ color: question ? "black" : "#9ca3af", lineHeight: "1.5" }}
      />
      <div className="flex justify-between items-center mt-2">
        <Tooltip title="Add file" arrow placement="left">
          <button className=" flex items-center justify-center w-10 h-10 rounded-full hover:bg-gray-200">
            <AttachFileIcon />
          </button>
        </Tooltip>
        <Tooltip title="Send" arrow placement="right">
          <button
            onClick={handleSend}
            className="flex items-center justify-center w-10 h-10 rounded-full hover:bg-gray-200"
          >
            <ArrowUpwardRoundedIcon className="text-gray-500" />
          </button>
        </Tooltip>
      </div>
    </div>
  );
}
