package com.beardygames.arcadetable;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.WindowManager;

public class PongActivity extends AppCompatActivity implements SensorEventListener {

    // Variables for sensor data
    private SensorManager mSensorManager;
    private Sensor rotationSensor;
    private double pitch;

    private boolean playerLeft;

    // Variables for sending and receiving data
    private SendDataThread sendThread;
    private ReceiveDataThread receiveThread;
    private AppCompatActivity activity;

    private View decorView;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pong);

        // Keeps the screen so that the app keeps running and keeps sending data
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        DataHandler.setGameRunning(true);
        playerLeft = DataHandler.getPlayerLeft();

        // This code is taken from: https://developer.android.com/training/system-ui/immersive.html
        decorView = getWindow().getDecorView();
        // Hide both the navigation bar and the status bar.
        // SYSTEM_UI_FLAG_FULLSCREEN is only available on Android 4.1 and higher, but as
        // a general rule, you should design your app to hide the status bar whenever you
        // hide the navigation bar.
        int uiOptions = View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);

        // needed so that the activity can be closed from the thread
        activity = this;

        // we use the game rotation vector to measure the pitch value of the smartphone
        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        rotationSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_GAME_ROTATION_VECTOR);
        pitch = 0;

        System.out.println("in der on create methode");
        // Thread-Handling
        sendThread = new SendDataThread(false);
        sendThread.start();
        receiveThread = new ReceiveDataThread();
        new Thread(receiveThread).start();
        new Thread(new WaitForInputThread()).start();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_GAME_ROTATION_VECTOR) {
            // Calculate the rotation matrix from the rotation vector
            float[] rotationMatrix = new float[9];
            SensorManager.getRotationMatrixFromVector(rotationMatrix, event.values);

            // Calculate the orientation from the rotation matrix
            final float[] orientationAngles = new float[3];
            SensorManager.getOrientation(rotationMatrix, orientationAngles);

            pitch = orientationAngles[1] * 360 / (2 * Math.PI);

            // calculate the speed for the game running on the raspberry pi
            int speed = (int) (pitch / 10);
            if (playerLeft){
                speed *= -1;
            }
            String data = "speed:" + speed;

            // Gives the data to the sendThread to send it to the raspberry pi
            sendThread.setData(data);
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
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
    protected void onResume() {
        super.onResume();
        mSensorManager.registerListener(this, rotationSensor, SensorManager.SENSOR_DELAY_GAME);
    }

    @Override
    protected void onPause() {
        super.onPause();
        mSensorManager.unregisterListener(this);
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
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    activity.finish();
                    break;
                }
            }
        }
    }

}
