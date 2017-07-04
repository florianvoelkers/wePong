package com.beardygames.arcadetable;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {

    private View decorView;
    private Animation blinking;
    private ImageView startImage;
    private ImageView playerOne;
    private ImageView playerTwo;
    private ImageView seperator;
    private boolean startPressed;
    private boolean readyForNewEvent;

    private Socket socket;

    private static final int SERVERPORT = 5000;
    private static final String SERVER_IP = "192.168.0.1";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        startPressed = false;

        decorView = getWindow().getDecorView();
        // Hide both the navigation bar and the status bar.
        // SYSTEM_UI_FLAG_FULLSCREEN is only available on Android 4.1 and higher, but as
        // a general rule, you should design your app to hide the status bar whenever you
        // hide the navigation bar.
        int uiOptions = View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);

        startImage = (ImageView) findViewById(R.id.start);
        playerOne = (ImageView) findViewById(R.id.player_one);
        playerOne.setVisibility(View.INVISIBLE);
        playerTwo = (ImageView) findViewById(R.id.player_two);
        playerTwo.setVisibility(View.INVISIBLE);
        seperator = (ImageView) findViewById(R.id.seperator);
        seperator.setVisibility(View.INVISIBLE);

        blinking = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.blinking);
        startImage.startAnimation(blinking);

        /*try {
            InetAddress serverAddr = InetAddress.getByName(SERVER_IP);
            socket = new Socket(serverAddr, SERVERPORT);
        } catch (UnknownHostException e1) {
            e1.printStackTrace();
        } catch (IOException e1) {
            e1.printStackTrace();
        }*/
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

    //Function to send the player to the server
    private void sendMessage(String str){
        try {
            PrintWriter out = new PrintWriter(new BufferedWriter(
                    new OutputStreamWriter(socket.getOutputStream())),
                    true);
            out.print(str);
            out.flush();

        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int x = (int) event.getX();
        int y = (int) event.getY();
        int width = DataHandler.getScreenWidth();
        int height = DataHandler.getScreenHeight();

        if (event.getActionMasked() == MotionEvent.ACTION_UP){
            readyForNewEvent = true;
        }

        if (readyForNewEvent) {
            // when start is clicked
            if (!startPressed) {
                if (y >= height * 0.66) {
                    readyForNewEvent = false;
                    startPressed = true;
                    startImage.clearAnimation();
                    startImage.setVisibility(View.INVISIBLE);
                    playerOne.setVisibility(View.VISIBLE);
                    playerTwo.setVisibility(View.VISIBLE);
                    seperator.setVisibility(View.VISIBLE);
                }
            } else {
                if (y >= height * 0.66) {
                    if (x <= width * 0.5) {
                        //sendMessage("player1");
                        System.out.println("player1");
                        DataHandler.setPlayerLeft(true);
                    } else {
                        //sendMessage("player2");
                        System.out.println("player2");
                        DataHandler.setPlayerLeft(false);
                    }
                    Intent intent = new Intent(this, GameMenuActivity.class);
                    startActivity(intent);
                }
            }
        }
        return super.onTouchEvent(event);
    }
}
