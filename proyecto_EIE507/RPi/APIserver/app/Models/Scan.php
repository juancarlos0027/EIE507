<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Scan extends Model
{
    use HasFactory;

    protected $fillable = [
        'sensor_id',
        'measure_unit_id',
        'amount'
    ];

    protected $cast = [
        // created_at without the Z at the end
        'created_at' => 'datetime:Y-m-d H:i:s'
    ];

    // Serializing the created_at attribute
    protected $appends = [
        'created_at_formatted'
    ];

    public function getCreatedAtFormattedAttribute(){
        return $this->created_at->format('Y-m-d H:i:s');
    }
}
