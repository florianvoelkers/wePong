package com.beardygames.arcadetable;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.annotation.Nullable;

public class PongActivity extends GameActivity implements SensorEventListener {

    // Variables for sensor data
    private SensorManager mSensorManager;
    private Sensor rotationSensor;
    private double pitch;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pong);

        // needed so that the activity can be closed from within the thread
        activity = this;

        // we use the game rotation vector to measure the pitch value of the smartphone
        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        rotationSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_GAME_ROTATION_VECTOR);
        pitch = 0;
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
    public void onAccuracyChanged(Sensor sensor, int accuracy) {}

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
}
