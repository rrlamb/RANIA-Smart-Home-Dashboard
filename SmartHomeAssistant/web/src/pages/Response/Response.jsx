import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useWebSocket } from "../../hooks/useWebSocket";
import "./Response.css";

const Response = () => {
  const [socketUrl] = useState("ws://localhost:8001/");
  const websocket = useWebSocket(socketUrl);

  const [response, setResponse] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    let timeoutId;

    if (websocket?.lastJsonMessage) {
      const waittime = websocket.lastJsonMessage.waittime ?? 0;

      timeoutId = setTimeout(
        () => navigate(websocket.lastJsonMessage.route),
        waittime * 1000
      );
    }

    if (websocket?.lastJsonMessage?.text) {
      setResponse((prevResponse) =>
        [prevResponse, websocket.lastJsonMessage.text].join(" ")
      );
    }

    return () => {
      clearTimeout(timeoutId);
    };
  }, [websocket?.lastJsonMessage, navigate]);

  return (
    <div>
      <h1 className="Response__text">{response}</h1>
    </div>
  );
};

export default Response;
