package com.beardygames.arcadetable;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

// Handles sending data to the server
public class SendDataThread extends Thread {

    private String data;
    private Socket socket;
    private volatile boolean onCommand;
    private volatile boolean dataSet;

    public SendDataThread(boolean onCommand){
        this.onCommand = onCommand;
        dataSet = false;
        socket = DataHandler.getServerSocket();
    }

    public void setData(String data){
        this.data = data;
        dataSet = true;
    }

    @Override
    public void run() {
        while(DataHandler.getGameRunning()){
            // onCommand determines whether or not sending data is a one time action
            if (onCommand){
                if (dataSet){
                    try {
                        PrintWriter out = new PrintWriter(new BufferedWriter(
                                new OutputStreamWriter(socket.getOutputStream())),
                                true);
                        out.print(data);
                        out.flush();
                        if (DataHandler.getIsTron()) {
                            data = "direction:none";
                            try {
                                Thread.sleep(50);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                        else {
                            data = "";
                            dataSet = false;
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
            else{
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                try {
                    PrintWriter out = new PrintWriter(new BufferedWriter(
                            new OutputStreamWriter(socket.getOutputStream())),
                            true);
                    out.print(data);
                    out.flush();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return;
    }
}
