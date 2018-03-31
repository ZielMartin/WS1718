package de.fhbi.mobappproj.gps_praesi;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

import java.util.Arrays;
import java.util.List;

import de.fhbi.mobappproj.gps_praesi.activities.LocationDemo1Activity;
import de.fhbi.mobappproj.gps_praesi.activities.LocationDemo2Activity;
import de.fhbi.mobappproj.gps_praesi.activities.MapsActivity1;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MAIN_ACTIVITY";

    private List<Class> myActivities = Arrays.asList(
            LocationDemo1Activity.class,
            LocationDemo2Activity.class,
            MapsActivity1.class
            );

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        createList();

    }
    private void createList() {
        for (final Class<?> activity : myActivities) {
            Button changeActivityTo = new Button(getApplicationContext());
            String buttonName = activity.toString().substring(activity.toString().lastIndexOf('.') + 1);
            changeActivityTo.setText(buttonName);

            changeActivityTo.setOnClickListener(view -> {
                Intent intent = new Intent(this, activity);
                startActivity(intent);
            });

            ((LinearLayout) findViewById(R.id.activity_main)).addView(changeActivityTo);

        }
    }
}
