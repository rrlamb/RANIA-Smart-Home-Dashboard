import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useWebSocket } from "../../hooks/useWebSocket";

import "./Idle.css";

const Idle = () => {
  const [socketUrl] = useState("ws://localhost:8001/");
  const websocket = useWebSocket(socketUrl);

  useEffect(() => {
    if (websocket?.lastMessage !== null) {
      console.log(websocket.lastMessage);
    }
  }, [websocket?.lastMessage]);

  const handleSendMessage = () => {
    websocket?.sendMessage("hello");
  };

  return (
    <div>
      <h1>Idle</h1>
      <Link to="/listening">Listening</Link>

      <button onClick={() => handleSendMessage()}>Send data</button>

      <h1 className="Idle__header">Say "Hey Rania"</h1>
    </div>
  );
};

export default Idle;
