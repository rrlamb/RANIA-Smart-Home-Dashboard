import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useWebSocket } from "../../hooks/useWebSocket";

import "./Idle.css";

const Idle = () => {
  const [socketUrl] = useState("ws://localhost:8001/");
  const websocket = useWebSocket(socketUrl);
  const navigate = useNavigate();

  useEffect(() => {
    if (websocket?.lastJsonMessage?.route) {
      navigate(websocket.lastJsonMessage.route);
    }
  }, [websocket?.lastJsonMessage, navigate]);

  return (
    <div>
      <h1 className="Idle__header">Say "Hey Rania"</h1>
    </div>
  );
};

export default Idle;
