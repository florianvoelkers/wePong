package com.beardygames.arcadetable;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class ReceiveDataThread implements Runnable {

    private volatile String data;
    private Socket socket;

    public ReceiveDataThread(){
        socket = DataHandler.getServerSocket();
        data = "";
    }

    public String getData(){
        return data;
    }

    @Override
    public void run() {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            data = in.readLine();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
