package com.example.aksalvashi.myapplication;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.Toast;
import com.example.aksalvashi.myapplication.SecondActivity;

import java.io.*;
import java.io.File;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "DemoInitialApp";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        setupLaunchButton();
    }
    //make the button do stuff
    //get the button

    private void setupLaunchButton() {
        Button btn = (Button) findViewById(R.id.btnDoMagic);

        //set what happens when you click the button
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.i(TAG, "This button is working");
                //Toast.makeText(getApplicationContext(), "Analyzing data: Launching 2nd", Toast.LENGTH_SHORT).show();
                //cant do that^^ bc get application context will only stay in this public void onClick and we need this whole class so
                Toast.makeText(getApplicationContext(), "Analyzing data: Launching 2nd", Toast.LENGTH_SHORT).show();

                //Launch the second activity
                Intent intent = new Intent(MainActivity.this, SecondActivity.class);
                startActivity(intent);
            }
        });

    }
}