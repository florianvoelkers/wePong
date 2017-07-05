package com.beardygames.arcadetable;

import java.net.Socket;

public class SendDataThread extends Thread {

    private String data;
    private Socket socket;

    public SendDataThread(){
        //socket = DataHandler.getServerSocket();
    }

    public void setData(String data){
        this.data = data;
    }

    @Override
    public void run() {
        while(DataHandler.getGameRunning()){
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
