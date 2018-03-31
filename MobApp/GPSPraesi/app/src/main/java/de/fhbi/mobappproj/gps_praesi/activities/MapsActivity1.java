package de.fhbi.mobappproj.gps_praesi.activities;

import android.Manifest;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.location.LocationProvider;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentActivity;
import android.util.Log;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import de.fhbi.mobappproj.gps_praesi.R;

public class MapsActivity1 extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;

    private static final int PERMISSIONS_ACCESS_FINE_LOCATION = 123;

    private static final String TAG = "Standortupdate";

    private LocationManager locationManager = null;
    private LocationListener locationListenerGPS = null;
    private LocationListener locationListenerNetwork = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps1);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera
        LatLng sydney = new LatLng(-34, 151);
        mMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Sydney"));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney));
    }

    private void registerListeners() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSIONS_ACCESS_FINE_LOCATION);
        } else {
            locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0, 0, locationListenerNetwork);
            locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, locationListenerGPS);
        }
    }

    @Override
    protected void onResume() {
        super.onResume();

        locationManager = getSystemService(LocationManager.class);
        locationListenerNetwork = new NetworkLocationListener();
        locationListenerGPS = new GPSLocationListener();

        registerListeners();
    }

    @Override
    protected void onPause() {
        super.onPause();

        if (locationManager != null) {
            if (locationListenerNetwork != null) {
                locationManager.removeUpdates(locationListenerNetwork);
                locationListenerNetwork = null;
            }

            if (locationListenerGPS != null) {
                locationManager.removeUpdates(locationListenerGPS);
                locationListenerGPS = null;
            }
            locationManager = null;
        }
    }


    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        if ((requestCode == PERMISSIONS_ACCESS_FINE_LOCATION) &&
                (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
            registerListeners();
        }
    }

    private class GPSLocationListener implements LocationListener {

        @Override
        public void onLocationChanged(Location location) {
            Log.i(TAG, "gps: " + location.toString());
            LatLng myPosition = new LatLng(location.getLatitude(), location.getLongitude());
            mMap.moveCamera(CameraUpdateFactory.newLatLng(myPosition));
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {
            switch (status) {
                case LocationProvider.OUT_OF_SERVICE:
                    break;
                case LocationProvider.TEMPORARILY_UNAVAILABLE:
                    break;
                case LocationProvider.AVAILABLE:
                    break;
            }
        }

        @Override
        public void onProviderEnabled(String provider) {
            Log.i(TAG, "GPS ENABLED");
        }

        @Override
        public void onProviderDisabled(String provider) {
            Log.i(TAG, "GPS DISABLED");
        }

    }

    private class NetworkLocationListener implements LocationListener {
        @Override
        public void onLocationChanged(Location location) {
            Log.i(TAG, "network: " + location.toString());
            LatLng myPosition = new LatLng(location.getLatitude(), location.getLongitude());
            mMap.moveCamera(CameraUpdateFactory.newLatLng(myPosition));
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {

        }

        @Override
        public void onProviderEnabled(String provider) {

        }

        @Override
        public void onProviderDisabled(String provider) {

        }
    }
}
