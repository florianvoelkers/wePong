package com.beardygames.arcadetable;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.provider.ContactsContract;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.MotionEvent;
import android.view.View;

public class GameMenuActivity extends AppCompatActivity {

    private View decorView;
    private boolean touchReady;
    private SendDataThread dataThread;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_game_menu);

        decorView = getWindow().getDecorView();
        // Hide both the navigation bar and the status bar.
        // SYSTEM_UI_FLAG_FULLSCREEN is only available on Android 4.1 and higher, but as
        // a general rule, you should design your app to hide the status bar whenever you
        // hide the navigation bar.
        int uiOptions = View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);


    }

    @Override
    protected void onResume() {
        super.onResume();
        dataThread = new SendDataThread(true);
        touchReady = true;
        DataHandler.setGameRunning(true);
        dataThread.start();
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

    private void selectGame(String game){
        final Intent intent;
        touchReady = false;
        if (game.equals("pong")){
            intent = new Intent(this, PongActivity.class);
        }
        else if (game.equals("air")){
            intent = new Intent(this, AirHockeyActivity.class);
        }
        else{
            intent = new Intent(this, TronActivity.class);
        }
        dataThread.setData("game:" + game);
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                startActivity(intent);
                DataHandler.setGameRunning(false);
                dataThread.interrupt();
            }
        }, 1000);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (touchReady) {
            int x = (int) event.getX();
            int width = DataHandler.getScreenWidth();
            int y = (int) event.getY();
            int height = DataHandler.getScreenHeight();

            if (y >= height * 0.66 && x <= width * 0.5) {
                selectGame("pong");
            } else if (y >= height * 0.66 && x >= width * 0.5) {
                selectGame("air");
            } else if (y <= height * 0.33) {
                selectGame("tron");
            }
        }

        return super.onTouchEvent(event);
    }
}
