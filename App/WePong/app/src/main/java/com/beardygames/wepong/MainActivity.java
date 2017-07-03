package com.beardygames.wepong;

import android.graphics.drawable.AnimationDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ImageView;

public class MainActivity extends AppCompatActivity {

    private MainView view;
    private ImageView startImage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        view = (MainView)findViewById(R.id.customView);

        startImage = (ImageView) findViewById(R.id.start);

        // set its background to our AnimationDrawable XML resource.
        startImage.setBackgroundResource(R.drawable.start_animation);

		/*
		 * Get the background, which has been compiled to an AnimationDrawable
		 * object.
		 */
        AnimationDrawable frameAnimation = (AnimationDrawable) startImage.getBackground();

        // Start the animation (looped playback by default).
        frameAnimation.start();
    }

}
