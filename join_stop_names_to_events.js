db.events.aggregate([
{ $match: { "vehicle": {$exists: true} } },
{ $limit: 2 },
{ $lookup:
	{
		from: 'stops',
		localField: 'vehicle.stopId',
		foreignField: 'stop_id',
		as: 'stop_info'
	}
},
{ $addFields: { "stop_name": { $arrayElemAt: [ '$stop_info', 0]}}},
{$out: "csv_export"}
])
