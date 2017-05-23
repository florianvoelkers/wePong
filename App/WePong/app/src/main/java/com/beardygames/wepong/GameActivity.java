package com.beardygames.wepong;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

public class GameActivity extends AppCompatActivity implements SensorEventListener {

    private GameView view;
    private SensorManager mSensorManager;
    private Sensor accelerometer;
    private Sensor rotationSensor;

    private double azimuth;
    private float [] accel;
    private boolean wifiEnabled;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_game);

        view = (GameView) findViewById(R.id.gameView);

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        accelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
        rotationSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_GAME_ROTATION_VECTOR);

        azimuth = 0;
        accel = new float[3];
        for (int i = 0; i < accel.length; i++){
            accel[i] = 0;
        }
    }

    public void setWifiEnabled(boolean isEnabled){
        wifiEnabled = isEnabled;
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_GAME_ROTATION_VECTOR) {
            // Umrechnung Rotationsvektor --> Rotationsmatrix
            float[] rotationMatrix = new float[9];
            SensorManager.getRotationMatrixFromVector(rotationMatrix, event.values);
            //Umrechnung Rotationsmatrix --> Orientierung (3 Winkel)
            final float[] orientationAngles = new float[3];
            SensorManager.getOrientation(rotationMatrix, orientationAngles);

            //Azimuth darstellen
            azimuth = orientationAngles[0] * 360 / (2 * Math.PI);
        }
        else if (event.sensor.getType() == Sensor.TYPE_LINEAR_ACCELERATION){
            accel[0] = event.values[0];// - gravity[0];
            accel[1] = event.values[1];// - gravity[1];
            accel[2] = event.values[2];// - gravity[2];
        }

        view.drawCanvas(azimuth, accel);
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    @Override
    protected void onResume() {
        super.onResume();
        mSensorManager.registerListener(this, rotationSensor, SensorManager.SENSOR_DELAY_NORMAL);
        mSensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    protected void onPause() {
        super.onPause();
        mSensorManager.unregisterListener(this);
    }
}
