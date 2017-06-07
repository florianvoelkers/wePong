package com.beardygames.wepong;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.PowerManager;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

public class GameActivity extends AppCompatActivity implements SensorEventListener {

    private SensorManager mSensorManager;
    private Sensor accelerometer;
    private Sensor rotationSensor;

    private Button player1Button;
    private Button player2Button;

    private Socket socket;

    private static final int SERVERPORT = 5000;
    private static final String SERVER_IP = "192.168.0.1";

    private double azimuth;
    private int startAngle;
    private int rangeLeft;
    private int rangeRight;
    private String upOrDown;
    private boolean playerLeft;
    private int accel;
    private int counter = 0;
    private int velocityCounter = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_game);

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        accelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
        rotationSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_GAME_ROTATION_VECTOR);

        player1Button = (Button)findViewById(R.id.player1);
        player2Button = (Button)findViewById(R.id.player2);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        azimuth = 0;
        accel = 0;

        new Thread(new ClientThread()).start();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_GAME_ROTATION_VECTOR) {
            counter++;
            // Umrechnung Rotationsvektor --> Rotationsmatrix
            float[] rotationMatrix = new float[9];
            SensorManager.getRotationMatrixFromVector(rotationMatrix, event.values);
            //Umrechnung Rotationsmatrix --> Orientierung (3 Winkel)
            final float[] orientationAngles = new float[3];
            SensorManager.getOrientation(rotationMatrix, orientationAngles);

            //Azimuth darstellen
            azimuth = orientationAngles[0] * 1440 / (2 * Math.PI);
            System.out.println("new azimuth: " + azimuth);
            if (counter == 1){
                startAngle = (int)azimuth;
                rangeLeft = startAngle - 90;
                rangeRight = startAngle + 90;

                if (rangeLeft < -180){
                    rangeLeft += 360;
                }

                if (rangeRight > 180){
                    rangeRight -= 360;
                }

                if (rangeLeft > rangeRight){
                    int cache = rangeLeft;
                    rangeLeft = rangeRight;
                    rangeRight = cache;
                }
            }
        }
        if (event.sensor.getType() == Sensor.TYPE_LINEAR_ACCELERATION){
            if (event.values[0] > accel){
                accel = (int)event.values[0];
            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    @Override
    protected void onResume() {
        super.onResume();
        mSensorManager.registerListener(this, rotationSensor, SensorManager.SENSOR_DELAY_GAME);
        mSensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_GAME);
    }

    @Override
    protected void onPause() {
        super.onPause();
        mSensorManager.unregisterListener(this);
    }

    class ClientThread implements Runnable {

        private void sendServerPlayer(String str, Socket socket){
            System.out.println("click");
            try {
                PrintWriter out = new PrintWriter(new BufferedWriter(
                        new OutputStreamWriter(socket.getOutputStream())),
                        true);
                //Create BufferedReader object for receiving messages from server.
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                out.print(str);
                out.flush();

                new Thread(new DataThread(socket)).start();

            } catch (UnknownHostException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        @Override
        public void run() {

            try {
                InetAddress serverAddr = InetAddress.getByName(SERVER_IP);

                socket = new Socket(serverAddr, SERVERPORT);

                player1Button.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        playerLeft = true;
                        sendServerPlayer("player1", socket);
                    }
                });

                player2Button.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        playerLeft = false;
                        sendServerPlayer("player2", socket);
                    }
                });

            } catch (UnknownHostException e1) {
                e1.printStackTrace();
            } catch (IOException e1) {
                e1.printStackTrace();
            }

        }

    }

    class DataThread implements Runnable{

        private Socket socket;

        public DataThread(Socket socket){
            this.socket = socket;
        }

        @Override
        public void run() {
            System.out.println("in send data");
            while (true){
                try {
                    velocityCounter++;
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                try {
                    PrintWriter out = new PrintWriter(new BufferedWriter(
                            new OutputStreamWriter(socket.getOutputStream())),
                            true);
                    if (playerLeft){
                        if (azimuth >= rangeLeft && azimuth <= rangeRight){
                            upOrDown = "down";
                        }
                        else {
                            upOrDown = "up";
                        }
                    }
                    else {

                        System.out.println("start: " + startAngle + " range: " + rangeLeft + " " + rangeRight + " azimuth: " + azimuth);
                        if (azimuth >= rangeLeft && azimuth <= rangeRight){
                            upOrDown = "up";
                        }
                        else {
                            upOrDown = "down";
                        }

                    }
                    System.out.println(upOrDown);
                    String data = upOrDown + ":" + accel;
                    if (velocityCounter == 15){
                        velocityCounter = 0;
                        accel = 0;
                    }
                    out.print(data);
                    out.flush();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

}
