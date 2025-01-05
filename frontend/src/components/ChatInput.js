import React, { useRef, useEffect, useState } from "react";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import ArrowUpwardRoundedIcon from "@mui/icons-material/ArrowUpwardRounded";
import Tooltip from "@mui/material/Tooltip";

export default function ChatInput({ question, onChange, onSubmit, disableInput }) {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const textAreaRef = useRef(null);

  const handleSend = () => {
    if (onSubmit && !disableInput) {
        onSubmit(question, selectedFiles); // Send all selected files
        onChange(""); // Clear the question input
        setSelectedFiles([]); // Clear selected files
    }
};


  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    if (selectedFiles.length + files.length > 5) {
      alert("You can upload a maximum of 5 files.");
      return;
    }
    setSelectedFiles([...selectedFiles, ...files]);
  };

  const removeFile = (index) => {
    const updatedFiles = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(updatedFiles);
  };

  useEffect(() => {
    if (textAreaRef.current) {
      textAreaRef.current.style.height = "auto";
      textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`;
    }
  }, [question]);

  return (
    <div className="flex flex-col w-full bg-gray-200 rounded-xl py-3 px-4">
      {/* File Display */}
      <div className="flex flex-wrap gap-2 mb-2">
        {selectedFiles.map((file, index) => (
          <div key={index} className="flex items-center bg-gray-300 rounded-lg px-3 py-1">
            <span className="text-sm mr-2">{file.name}</span>
            <button
              className="text-red-500"
              onClick={() => removeFile(index)}
            >
              &times;
            </button>
          </div>
        ))}
      </div>

      {/* Input Box */}
      <textarea
        ref={textAreaRef}
        placeholder="Nhập câu hỏi"
        value={question}
        onChange={(e) => onChange(e.target.value)}
        className="flex-grow bg-transparent bg-gray w-full border-none outline-none text-gray-700 placeholder-gray-500 resize-none overflow-y-auto max-h-32"
        rows={1}
        style={{ color: question ? "black" : "#9ca3af", lineHeight: "1.5" }}
      />

      {/* Action Buttons */}
      <div className="flex justify-between items-center mt-2">
        <Tooltip title="Add file" arrow placement="left">
          <label className="flex items-center justify-center w-10 h-10 rounded-full hover:bg-gray-300 cursor-pointer">
            <AttachFileIcon />
            <input
              type="file"
              multiple
              onChange={handleFileChange}
              className="hidden"
            />
          </label>
        </Tooltip>
        <Tooltip title="Send" arrow placement="right">
          <button
            onClick={handleSend}
            className="flex items-center justify-center w-10 h-10 rounded-full hover:bg-gray-300"
          >
            <ArrowUpwardRoundedIcon className="text-gray-500" />
          </button>
        </Tooltip>
      </div>
    </div>
  );
}
