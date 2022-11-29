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
        //dd($request->all());
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

    public Function getSensorData(Request $request, $sensor_id){
        $sensor_id = $request->sensor_id;
        
        $sensor = Sensor::find($sensor_id);
        if($sensor){
            // Traer los ultimos 20 registros
            $scans = Scan::where('sensor_id', $sensor_id)->orderBy('created_at', 'desc')->take(20)->get();
            return response()->json(['data' => $scans], 200);
        }
        else{
            return response()->json(['error' => 'Sensor no encontrado'], 404);
        }
    }
}
