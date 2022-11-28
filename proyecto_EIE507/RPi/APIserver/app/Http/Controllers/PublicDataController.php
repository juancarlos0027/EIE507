<?php

namespace App\Http\Controllers;
use App\Models\Sensor;

use Illuminate\Http\Request;

class PublicDataController extends Controller
{
    public function store(Request $request){
        // the request is sent in a payload by the esp8266, so we need to decode it
        $payload = json_decode($request->payload, true);
        Log::info($payload);
        Log::info($request);

        if($sensor = Scan::create(
            [
                'sensor_id' => $payload['sensor_id'],
                'measure_unit_id' => $payload['measure_unit_id'],
                'amount' => $payload['amount']
            ]
        )){
            return response()->json('OK', 200);
        }
        else{
            return response()->json(['error' => 'Error al guardar la información'], 500);
        }
    }
}
