package com.beardygames.arcadetable;

import android.content.res.Resources;

import java.net.Socket;

// Handles all the data that has to be saved, e.g. which player the user is, screen sizes or the socket
public class DataHandler {

    private static boolean playerLeft;
    private static Socket serverSocket;
    private static boolean gameRunning;
    private static boolean isTron;

    public static void setIsTron(boolean value){ isTron = value; };

    public static boolean getIsTron(){ return isTron; }

    public static void setPlayerLeft(boolean value){playerLeft = value;}

    public static boolean getPlayerLeft(){return playerLeft;}

    public static void setSocket(Socket socket){serverSocket = socket;}

    public static Socket getServerSocket(){
        return serverSocket;
    }

    public static void setGameRunning(boolean gameRuns){
        gameRunning = gameRuns;
    }

    public static boolean getGameRunning(){
        return gameRunning;
    }

    public static int getScreenWidth() {return Resources.getSystem().getDisplayMetrics().widthPixels;}

    public static int getScreenHeight() {return Resources.getSystem().getDisplayMetrics().heightPixels;}
}
