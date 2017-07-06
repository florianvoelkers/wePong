package com.beardygames.arcadetable;

import java.net.Socket;

public class SendDataThread extends Thread {

    private String data;
    private Socket socket;
    private boolean isTron;
    private boolean dataSet;

    public SendDataThread(boolean isTron){
        this.isTron = isTron;
        dataSet = false;
        //socket = DataHandler.getServerSocket();
    }

    public void setData(String data){
        this.data = data;
        dataSet = true;
    }

    @Override
    public void run() {
        while(DataHandler.getGameRunning()){
            if (isTron){
                if (dataSet){
                    /*try {
                    PrintWriter out = new PrintWriter(new BufferedWriter(
                            new OutputStreamWriter(serverSocket.getOutputStream())),
                            true);*/

                    System.out.println(data);
                    /*
                    out.print(data);
                    out.flush();*/
                    data = "";
                    dataSet = false;
                /*} catch (IOException e) {
                    e.printStackTrace();
                }*/
                }
            }
            else{
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                /*try {
                    PrintWriter out = new PrintWriter(new BufferedWriter(
                            new OutputStreamWriter(serverSocket.getOutputStream())),
                            true);*/

                    System.out.println(data);
                    /*
                    out.print(data);
                    out.flush();*/
                /*} catch (IOException e) {
                    e.printStackTrace();
                }*/
            }
        }
    }
}
