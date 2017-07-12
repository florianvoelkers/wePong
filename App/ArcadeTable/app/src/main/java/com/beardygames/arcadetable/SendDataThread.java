package com.beardygames.arcadetable;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

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
            if (onCommand){
                if (dataSet){
                    try {
                        PrintWriter out = new PrintWriter(new BufferedWriter(
                                new OutputStreamWriter(socket.getOutputStream())),
                                true);
                        out.print(data);
                        out.flush();
                        data = "";
                        dataSet = false;
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
