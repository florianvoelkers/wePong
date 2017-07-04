package com.beardygames.arcadetable;

import android.content.res.Resources;

// Handles all the data that has to be saved, e.g. which player the user is or screen sizes
public class DataHandler {

    private static boolean playerLeft;

    public static void setPlayerLeft(boolean value){
        playerLeft = value;
    }

    public static boolean getPlayerLeft(){
        return playerLeft;
    }

    public static int getScreenWidth() {
        return Resources.getSystem().getDisplayMetrics().widthPixels;
    }

    public static int getScreenHeight() {
        return Resources.getSystem().getDisplayMetrics().heightPixels;
    }
}
