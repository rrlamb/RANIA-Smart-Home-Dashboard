import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useWebSocket } from "../../hooks/useWebSocket";
import "./Loading.css";

const Loading = () => {
  const [socketUrl] = useState("ws://localhost:8001/");
  const websocket = useWebSocket(socketUrl);
  const navigate = useNavigate();

  return (
    <div>
      <h1 className="Loading__container">Processing your request...</h1>
    </div>
  );
};

export default Loading;
