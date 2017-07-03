package com.beardygames.wepong;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Picture;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;
import android.view.animation.AlphaAnimation;
import android.view.animation.Animation;
import android.view.animation.LinearInterpolator;
import android.widget.ImageView;

public class MainView extends View {

    private Rect joinGameButton;
    private Rect instructionsButton;
    private Rect setNameButton;
    private Rect exitButton;

    public MainView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    protected void onDraw(Canvas canvas){
        super.onDraw(canvas);

        Paint paint = new Paint();
        paint.setStyle(Paint.Style.FILL);
        paint.setColor(Color.WHITE);
        paint.setStrokeWidth(9);

        int centerX = (int) (canvas.getWidth() * 0.5f);
        int centerY = (int) (canvas.getHeight() * 0.5f);
        int height = canvas.getHeight();
        int width = canvas.getWidth();

        Bitmap background = BitmapFactory.decodeResource(getResources(), R.drawable.background);
        canvas.drawBitmap(background, centerX - background.getWidth() * 0.5f, centerY - background.getHeight() * 0.5f, paint);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int x = (int) event.getX();
        int y = (int) event.getY();

        if (joinGameButton.contains(x, y)){
            Intent intent = new Intent(getContext(), GameActivity.class);
            getContext().startActivity(intent);
        }
        else if (instructionsButton.contains(x, y)){
            Intent intent = new Intent(getContext(), InstructionsActivity.class);
            getContext().startActivity(intent);
        }
        else if (setNameButton.contains(x, y)){
            Intent intent = new Intent(getContext(), SetNameActivity.class);
            getContext().startActivity(intent);
        }
        else if (exitButton.contains(x, y)){
            System.exit(0);
        }

        return super.onTouchEvent(event);
    }
}
