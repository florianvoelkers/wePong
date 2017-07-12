package com.beardygames.arcadetable;

import android.os.Bundle;
import android.os.StrictMode;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;

public class AirHockeyActivity extends AppCompatActivity {

    private View decorView;
    private boolean playerLeft;

    //Variables for the position of the touch event
    private int posX;
    private int posY;
    private int width;
    private int height;

    //Variables for sending and receiving data
    private SendDataThread sendThread;
    private ReceiveDataThread receiveThread;
    private AppCompatActivity activity;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_air_hockey);

        // Keeps the screen so that the app keeps running and keeps sending data
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        DataHandler.setGameRunning(true);
        playerLeft = DataHandler.getPlayerLeft();

        activity = this;

        // This code is taken from: https://developer.android.com/training/system-ui/immersive.html
        decorView = getWindow().getDecorView();
        // Hide both the navigation bar and the status bar.
        // SYSTEM_UI_FLAG_FULLSCREEN is only available on Android 4.1 and higher, but as
        // a general rule, you should design your app to hide the status bar whenever you
        // hide the navigation bar.
        int uiOptions = View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);

        //sets the start position
        posX = 50;
        posY = 100;
        width = DataHandler.getScreenWidth();
        height = DataHandler.getScreenHeight();

        //Thread-Handling
        sendThread = new SendDataThread(false);
        sendThread.start();
        receiveThread = new ReceiveDataThread();
        new Thread(receiveThread).start();
        new Thread(new WaitForInputThread()).start();
    }

    // This code is taken from: https://developer.android.com/training/system-ui/immersive.html
    // The IMMERSIVE_STICKY flag, and the user swipes to display the system bars.
    // Semi-transparent bars temporarily appear and then hide again.
    // The act of swiping doesn't clear any flags, nor does it trigger your system UI visibility change listeners,
    // because the transient appearance of the system bars isn't considered a UI visibility change.
    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            decorView.setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        }
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

    // Always waiting for the Server to send "end", when it does go back to the menu screen
    class WaitForInputThread implements Runnable {

        @Override
        public void run() {
            while(true){
                String data = receiveThread.getData();
                if (data.equals("end")){
                    sendThread.interrupt();
                    try {
                        Thread.sleep(1000);
                        activity.finish();
                        break;
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }
            }
        }
    }
}
