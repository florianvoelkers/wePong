package com.beardygames.arcadetable;

import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Scanner;

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
            Scanner input = new Scanner(new InputStreamReader(socket.getInputStream()));
            data = input.next();
            if (data.equals("end")){
                DataHandler.setGameRunning(false);
                //input.close();
                return;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}