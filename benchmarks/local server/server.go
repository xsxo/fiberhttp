package main

import (
	"fmt"
	"net"
	"strconv"
)

const (
	HOST = "localhost"
	PORT = 80
)

func recvSend(conn net.Conn) {
	defer conn.Close()
	buffer := make([]byte, 1024)

	for {
		_, err := conn.Read(buffer)
		if err != nil {
			break
		}

		data := "random="
		response := "HTTP/1.1 200 OK\r\n" +
			"Content-Type: text/html\r\n" +
			"Content-Length: " + strconv.Itoa(len(data)) + "\r\n" +
			"\r\n" +
			data

		_, err = conn.Write([]byte(response))
		if err != nil {
			break
		}
	}
}

func main() {
	listener, err := net.Listen("tcp", fmt.Sprintf("%s:%d", HOST, PORT))
	if err != nil {
		fmt.Println("Error starting server:", err)
		return
	}
	defer listener.Close()

	fmt.Printf("Server listening on http://%s:%d\n", HOST, PORT)

	for {
		clientConn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}
		go recvSend(clientConn)
	}
}
