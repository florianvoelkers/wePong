package com.beardygames.wepong;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.PorterDuff;
import android.util.AttributeSet;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

public class GameView extends SurfaceView implements SurfaceHolder.Callback {

    private SurfaceHolder surfaceHolder;

    public GameView(Context context, AttributeSet attrs){
        super(context, attrs);
        surfaceHolder = getHolder();
        surfaceHolder.addCallback(this);
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder) {

    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {

    }

    public void drawCanvas(double angle){
        if (angle < 0){
            angle = angle + 360;
        }
        Canvas canvas = surfaceHolder.lockCanvas();
        Paint paint = new Paint();
        paint.setStyle(Paint.Style.FILL);
        paint.setColor(Color.WHITE);
        paint.setTextSize(32);
        paint.setTextAlign(Paint.Align.CENTER);

        canvas.drawColor(0, PorterDuff.Mode.CLEAR);
        canvas.drawText("Angle: " + (int)angle, canvas.getWidth() * 0.5f, canvas.getHeight() * 0.25f, paint);

        surfaceHolder.unlockCanvasAndPost(canvas);
    }
}
