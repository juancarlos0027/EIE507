<?php

namespace App\Http\Controllers;
use App\Models\Sensor;
use App\Models\Scan;
use Illuminate\Support\Facades\Log;
use Illuminate\Http\Request;

class PublicDataController extends Controller
{
    public function store(Request $request){
        // the request is sent in a payload by the esp8266, so we need to decode it
        $payload = $request->all();

        if($sensor = Scan::create(
            [
                'sensor_id' => $payload['sensor_id'],
                'measure_unit_id' => $payload['measure_unit_id'],
                'amount' => $payload['amount']
            ]
        )){
            // if the sensor is created, we return a 200 status code
            return response()->json(['status' => 'ok'], 200);
        }
        else{
            return response()->json(['error' => 'Error al guardar la información'], 500);
        }
    }
}
