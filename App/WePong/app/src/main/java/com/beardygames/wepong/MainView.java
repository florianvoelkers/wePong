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

        canvas.drawLine(5, 0, 5, height, paint);
        canvas.drawLine(width - 5, 0, width - 5, height, paint);
        canvas.drawLine(0, centerY - 5,width, centerY - 5, paint);

        paint.setTextSize(172);
        paint.setTextAlign(Paint.Align.CENTER);
        canvas.drawText("wePong", centerX, centerY * 0.42f, paint);

        Bitmap title = BitmapFactory.decodeResource(getResources(), R.drawable.title);
        canvas.drawBitmap(title, centerX - title.getWidth() * 0.5f, height * 0.25f - title.getHeight() * 0.5f, paint);

        paint.setStyle(Paint.Style.STROKE);

        joinGameButton = new Rect(160, centerY + 80, width - 160, centerY + 220);
        canvas.drawRect(joinGameButton, paint);

        instructionsButton = new Rect(160, centerY + 260, width - 160, centerY + 400);
        canvas.drawRect(instructionsButton, paint);

        setNameButton = new Rect(160, centerY + 440, width - 160, centerY + 580);
        canvas.drawRect(setNameButton, paint);

        exitButton = new Rect(160, centerY + 620, width - 160, centerY + 760);
        canvas.drawRect(exitButton, paint);

        paint.setStyle(Paint.Style.FILL);
        paint.setTextSize(72);
        canvas.drawText("Join Game", centerX, joinGameButton.centerY() + 16, paint);
        canvas.drawText("Instructions", centerX, instructionsButton.centerY() + 16, paint);
        canvas.drawText("Set Name", centerX, setNameButton.centerY() + 16, paint);
        canvas.drawText("Exit", centerX, exitButton.centerY() + 16, paint);
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

        }
        else if (exitButton.contains(x, y)){
            System.exit(0);
        }

        return super.onTouchEvent(event);
    }
}
