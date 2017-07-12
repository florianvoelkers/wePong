package com.beardygames.arcadetable;

import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Scanner;

// Handles receiving data from the server and stops running after receiving it
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
        while(!data.equals("end"))
            try {
                Scanner input = new Scanner(new InputStreamReader(socket.getInputStream()));
                System.out.println("warte auf input");
                data = input.next();
                System.out.println("input  da: " + data);
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
