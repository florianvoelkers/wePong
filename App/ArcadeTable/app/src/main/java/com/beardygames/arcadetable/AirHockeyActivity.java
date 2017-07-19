package com.beardygames.arcadetable;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.MotionEvent;

public class AirHockeyActivity extends GameActivity {

    //Variables for the position of the touch event
    private int posX;
    private int posY;
    private int width;
    private int height;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_air_hockey);

        // needed so that the activity can be closed from within the thread
        activity = this;

        //sets the start position
        posX = 50;
        posY = 100;
        width = DataHandler.getScreenWidth();
        height = DataHandler.getScreenHeight();
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        // inverted positions in the python game
        posY = (int) (event.getX() / width * 93);
        posX = (int) (event.getY() / height * 101);

        if (playerLeft){
            posX = (posX - 100) * -1;
        }
        else{
            posY = (posY - 100) * -1;
        }
        sendThread.setData(posX + ":" + posY);
        return super.onTouchEvent(event);
    }
}
