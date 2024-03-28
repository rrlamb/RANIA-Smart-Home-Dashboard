import React, {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useRef,
} from "react";
import useWS from "react-use-websocket";

const WebSocketContext = createContext({});

const WebSocketProvider = ({ socketUrl, children }) => {
  const didUnmount = useRef(false);

  const { sendMessage, lastMessage, readyState, getWebSocket } = useWS(
    socketUrl,
    {
      retryOnError: true,
      reconnectAttempts: 10,
      // Reconnect pattern of 0, 1, 2, 4, 8, 10, 10, 10...
      reconnectInterval: (attemptNumber) =>
        Math.min(Math.pow(2, attemptNumber) * 1000, 10000),
      share: true,
      shouldReconnect: () => didUnmount.current,
    }
  );

  useEffect(() => {
    return () => {
      didUnmount.current = true;
    };
  }, []);

  const memoizedValue = useMemo(
    () => ({
      sendMessage,
      lastMessage,
      readyState,
      getWebSocket,
    }),
    [getWebSocket, lastMessage, readyState, sendMessage]
  );

  return (
    <WebSocketContext.Provider value={memoizedValue}>
      {children}
    </WebSocketContext.Provider>
  );
};

const useWebSocket = () => {
  return useContext(WebSocketContext);
};

export { WebSocketProvider, useWebSocket };
