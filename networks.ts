type SocketData = { sessionId: string };

Bun.listen<SocketData>({
  hostname: "localhost",
  port: 8080,
  socket: {
    data(socket, data) {
      console.log(data.toString());
      socket.write("HTTP/1.1 200 OK\r\n");
      socket.write("Connection: close\r\n");
      socket.write("Server: goonbox\r\n");
      socket.write("Content-Type: text/plain; charset=UTF-8\r\n");
      socket.write("\r\n");
      socket.write("cauky\r\n");
      socket.write("\r\n");
      socket.end("\r\n");
    },
  },
});
