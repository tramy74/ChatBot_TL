import React from "react";
import AddIcon from "@mui/icons-material/Add";
import Tooltip from "@mui/material/Tooltip";
import Button from "@mui/material/Button";

const Sidebar = ({ chatSessions, currentSession, onNewChat, onSelectSession }) => {
  return (
    <div className="w-1/4 bg-gray-200 p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Chat Sessions</h2>
        <Tooltip title="New chat" arrow>
          <Button
            variant="contained"
            color="primary"
            onClick={onNewChat}
            className="bg-blue-500 text-white px-2 py-1 rounded-md"
          >
            <AddIcon />
          </Button>
        </Tooltip>
      </div>
      <div className="space-y-2 overflow-y-auto max-h-screen">
        {chatSessions.map((session, index) => (
          <div
            key={index}
            onClick={() => onSelectSession(session)}
            className={`p-2 bg-white rounded-md shadow cursor-pointer ${
              currentSession && currentSession.id === session.id
                ? "bg-blue-100"
                : ""
            }`}
          >
            <p className="font-semibold truncate">
              {session.name || `Session ${index + 1}`}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
