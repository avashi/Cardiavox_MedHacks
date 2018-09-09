package com.example.aksalvashi.myapplication;

import android.content.Intent;
import android.os.Environment;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.Closeable;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import org.json.JSONObject;

public class SecondActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        setupLaunchButton();
        setupLaunchButton2();
        String response = "";
        int framesRead = 0;
        WavFile wavFile = null;
//        try {
//            wavFile = WavFile.openWavFile(new File("C:/Desktop/audio.wav"));
//            int numChannels = wavFile.getNumChannels();
//             //Create a buffer of 100 frames
//            double[] buffer = new double[100 * numChannels];
//             //Read frames into buffer
//            framesRead = wavFile.readFrames(buffer, 100);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();

        StrictMode.setThreadPolicy(policy);
            File file = new File(Environment.getExternalStorageDirectory().getAbsolutePath()+"/Desktop/audios.mp4");
        this.uploadCloud(1);
            try {
            SecondActivity hce = new SecondActivity();
            response = hce.get("http://35.196.93.110");
        } catch(IOException ioe) {
            ioe.printStackTrace();
        }
        //        } catch (IOException e) {
//            e.printStackTrace();
//        } catch (WavFileException e) {
//            e.printStackTrace();
//        }
        TextView textView = (TextView)findViewById(R.id.text_view);
        textView.setText(response);

    }


    private void setupLaunchButton() {
        Button btn = (Button) findViewById(R.id.button2);

        //goes back to first screen
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Log.i(TAG, "This button is working");
                //Toast.makeText(getApplicationContext(), "Analyzing data: Launching 2nd", Toast.LENGTH_SHORT).show();
                //cant do that^^ bc get application context will only stay in this public void onClick and we need this whole class so
                Toast.makeText(getApplicationContext(), "Recording Downloaded", Toast.LENGTH_SHORT).show();

                //Launch the second activity
                Intent intent = new Intent(SecondActivity.this, MainActivity.class);
                startActivity(intent);
            }
        });
    }

    private void setupLaunchButton2() {
        Button btn = (Button) findViewById(R.id.button);

        //goes back to first screen
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Log.i(TAG, "This button is working");
                //Toast.makeText(getApplicationContext(), "Analyzing data: Launching 2nd", Toast.LENGTH_SHORT).show();
                //cant do that^^ bc get application context will only stay in this public void onClick and we need this whole class so
                Toast.makeText(getApplicationContext(), "Record Again!", Toast.LENGTH_SHORT).show();

                //Launch the second activity
                Intent intent = new Intent(SecondActivity.this, MainActivity.class);
                startActivity(intent);
            }
        });
    }

    public static void uploadCloud(int wavFile) {
        URL url;
        try {
            url = new URL("https://www.googleapis.com/upload/storage/v1/b/steady-petal-209319-ml-engine/o?uploadType=media&name=testwave");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "MIME");
//            ByteBuffer b = ByteBuffer.allocate(4);
//            //b.order(ByteOrder.BIG_ENDIAN); // optional, the initial order of a byte buffer is always BIG_ENDIAN.
//            b.putInt(wavFile);
//            byte[] input = b.array();
//
            OutputStream os = conn.getOutputStream();
//            os.write(input);
            os.flush();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (ProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    public String get(String getUrl) throws IOException {
        URL url = new URL(getUrl);
        String val;
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");
        val = this.read(con.getInputStream());
        //put if statements here?
        System.out.println(val);
        val = val.substring(31,43);
        System.out.println(val);
        String message = "You May Have";

        if(val.equals("0")){
            message = "artifact";
        }
        else if (val.equals("2")){
            message = "murmur";
        }
        else if (val.equals("1")){
            message = "normal";
        }
        return message;
    }

    private String read(InputStream is) throws IOException {
        BufferedReader in = null;
        String inputLine;
        StringBuilder body = null;
        try {
            in = new BufferedReader(new InputStreamReader(is));

            body = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                body.append(inputLine);
            }
            in.close();
        } catch(IOException ioe) {
            ioe.printStackTrace();
        } finally {
            this.closeQuietly(in);
        }
        return body.toString();
    }

    protected void closeQuietly(Closeable closeable) {
        try {
            if( closeable != null ) {
                closeable.close();
            }
        } catch(IOException ex) {
            ex.printStackTrace();
        }
    }

}
