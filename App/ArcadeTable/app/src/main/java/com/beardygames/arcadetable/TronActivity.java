package com.beardygames.arcadetable;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.MotionEvent;

public class TronActivity extends GameActivity {

    // Variables for handling the touch events
    private boolean actionDone;
    private String direction;
    private int width;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tron);

        // needed so that the activity can be closed from within the thread
        activity = this;

        actionDone = false;
        direction = "";
        width = DataHandler.getScreenWidth();
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (event.getActionMasked() == MotionEvent.ACTION_DOWN){
            if (!actionDone){
                actionDone = true;
                // display is split in two halves
                if (event.getX() <= width * 0.5){
                    direction = "left";
                }
                else {
                    direction = "right";
                }
                String data = "direction:" + direction;
                sendThread.setData(data);
            }
        }
        else if (event.getActionMasked() == MotionEvent.ACTION_UP){
            actionDone = false;
        }
        return super.onTouchEvent(event);
    }
}
