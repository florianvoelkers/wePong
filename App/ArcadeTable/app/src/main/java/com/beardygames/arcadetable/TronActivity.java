package com.beardygames.arcadetable;

import android.os.Bundle;
import android.os.StrictMode;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;

public class TronActivity extends AppCompatActivity {

    private View decorView;
    private boolean actionDone;
    private String direction;

    private int width;

    private SendDataThread sendThread;
    private ReceiveDataThread receiveThread;
    private AppCompatActivity activity;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tron);

        // Keeps the screen so that the app keeps running and keeps sending data
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        DataHandler.setGameRunning(true);

        decorView = getWindow().getDecorView();
        // Hide both the navigation bar and the status bar.
        // SYSTEM_UI_FLAG_FULLSCREEN is only available on Android 4.1 and higher, but as
        // a general rule, you should design your app to hide the status bar whenever you
        // hide the navigation bar.
        int uiOptions = View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);

        activity = this;

        actionDone = false;
        direction = "";
        width = DataHandler.getScreenWidth();

        sendThread = new SendDataThread(false);
        sendThread.start();
        receiveThread = new ReceiveDataThread();
        new Thread(receiveThread).start();
        new Thread(new WaitForInputThread()).start();
    }

    // The IMMERSIVE_STICKY flag, and the user swipes to display the system bars.
    // Semi-transparent bars temporarily appear and then hide again.
    // The act of swiping doesn't clear any flags, nor does it trigger your system UI visibility change listeners,
    // because the transient appearance of the system bars isn't considered a UI visibility change.
    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            decorView.setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        }
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {

        if (event.getActionMasked() == MotionEvent.ACTION_DOWN){
            if (!actionDone){
                actionDone = true;
                if (event.getX() <= width * 0.5){
                    direction = "left";
                }
                else {
                    direction = "right";
                }
                String data = "direction:" + direction;
                dataThread.setData(data);
            }
        }
        else if (event.getActionMasked() == MotionEvent.ACTION_UP){
            actionDone = false;
        }

        return super.onTouchEvent(event);
    }

    // Always waiting for the Server to send "end", when it does go back to the menu screen
    class WaitForInputThread implements Runnable {

        @Override
        public void run() {
            while(true){
                String data = receiveThread.getData();
                if (data.equals("end")){
                    System.out.println("we are the world!");
                    sendThread.interrupt();
                    try {
                        Thread.sleep(1000);
                        activity.finish();
                        System.out.println("activity finished");
                        break;
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }
            }
        }
    }
}
