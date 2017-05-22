package com.beardygames.wepong;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.view.View;

public class CustomView extends View {

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

        canvas.drawLine(5, 0, 5, canvas.getHeight(), paint);
        canvas.drawLine(canvas.getWidth() - 5, 0, canvas.getWidth() - 5, canvas.getHeight(), paint);

    }
}
