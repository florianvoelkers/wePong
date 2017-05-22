package com.beardygames.wepong;

import android.content.Context;
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
import android.widget.ImageView;

public class CustomView extends View {

    private Rect joinGameButton;

    public CustomView(Context context, AttributeSet attrs) {
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

        canvas.drawLine(5, 0, 5, height, paint);
        canvas.drawLine(width - 5, 0, width - 5, height, paint);
        canvas.drawLine(0, centerY - 5,width, centerY - 5, paint);

        Bitmap title = BitmapFactory.decodeResource(getResources(), R.drawable.title);
        canvas.drawBitmap(title, centerX - title.getWidth() * 0.5f, height * 0.25f - title.getHeight() * 0.5f, paint);

        paint.setStyle(Paint.Style.STROKE);
        joinGameButton = new Rect(160, centerY + 120, width - 160, centerY + 280);
        canvas.drawRect(joinGameButton, paint);

    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int x = (int) event.getX();
        int y = (int) event.getY();

        if (joinGameButton.contains(x, y)){
            
        }

        return super.onTouchEvent(event);
    }
}
