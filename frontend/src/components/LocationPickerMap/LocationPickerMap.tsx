import { useState, useEffect, useCallback, useRef } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix para el icono de Leaflet en React
const markerIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

interface LocationPickerMapProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (lat: number, lng: number, address?: string) => void;
  initialLat?: number;
  initialLng?: number;
}

interface DraggableMarkerProps {
  position: [number, number];
  onPositionChange: (lat: number, lng: number) => void;
}

function DraggableMarker({ position, onPositionChange }: DraggableMarkerProps) {
  const [markerPosition, setMarkerPosition] = useState<[number, number]>(position);

  useEffect(() => {
    setMarkerPosition(position);
  }, [position]);

  const eventHandlers = {
    dragend(e: L.DragEndEvent) {
      const marker = e.target as L.Marker;
      const pos = marker.getLatLng();
      setMarkerPosition([pos.lat, pos.lng]);
      onPositionChange(pos.lat, pos.lng);
    },
  };

  return (
    <Marker
      position={markerPosition}
      icon={markerIcon}
      draggable={true}
      eventHandlers={eventHandlers}
    />
  );
}

function MapClickHandler({ onMapClick }: { onMapClick: (lat: number, lng: number) => void }) {
  useMapEvents({
    click(e) {
      onMapClick(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

function RecenterButton({ position }: { position: [number, number] }) {
  const map = useMap();
  
  const handleRecenter = useCallback(() => {
    map.flyTo(position, map.getZoom());
  }, [map, position]);

  return (
    <button
      onClick={handleRecenter}
      className="absolute bottom-20 right-4 z-[1000] bg-white p-3 rounded-full shadow-lg hover:bg-gray-100 transition-colors"
      title="Centrar en marcador"
    >
      <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    </button>
  );
}

export function LocationPickerMap({
  isOpen,
  onClose,
  onConfirm,
  initialLat = -12.0464,
  initialLng = -77.0428,
}: LocationPickerMapProps) {
  const [selectedPosition, setSelectedPosition] = useState<[number, number]>([initialLat, initialLng]);
  const [address, setAddress] = useState<string>('');
  const [isLoadingAddress, setIsLoadingAddress] = useState(false);
  const [mapKey, setMapKey] = useState(0);
  const mapContainerRef = useRef<HTMLDivElement>(null);

  // Regenerar key del mapa cuando se abre para evitar problemas de DOM
  useEffect(() => {
    if (isOpen) {
      setMapKey(prev => prev + 1);
      setSelectedPosition([initialLat, initialLng]);
      fetchAddress(initialLat, initialLng);
    }
  }, [isOpen, initialLat, initialLng]);

  const fetchAddress = useCallback(async (lat: number, lng: number) => {
    setIsLoadingAddress(true);
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`,
        { headers: { 'Accept-Language': 'es' } }
      );
      const data = await response.json();
      setAddress(data.display_name || 'Ubicación seleccionada');
    } catch {
      setAddress('Ubicación seleccionada');
    } finally {
      setIsLoadingAddress(false);
    }
  }, []);

  const handlePositionChange = useCallback((lat: number, lng: number) => {
    setSelectedPosition([lat, lng]);
    fetchAddress(lat, lng);
  }, [fetchAddress]);

  const handleConfirm = useCallback(() => {
    onConfirm(selectedPosition[0], selectedPosition[1], address);
    onClose();
  }, [selectedPosition, address, onConfirm, onClose]);

  const handleGetCurrentLocation = useCallback(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;
          setSelectedPosition([lat, lng]);
          fetchAddress(lat, lng);
        },
        () => {
          alert('No se pudo obtener tu ubicación');
        },
        { enableHighAccuracy: true, timeout: 10000 }
      );
    }
  }, [fetchAddress]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl mx-4 overflow-hidden animate-slide-up">
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">Selecciona tu ubicación</h3>
              <p className="text-blue-100 text-sm">Arrastra el marcador o toca el mapa</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-white/80 hover:text-white p-2 rounded-full hover:bg-white/10 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="relative h-80" ref={mapContainerRef}>
          <MapContainer
            key={mapKey}
            center={selectedPosition}
            zoom={15}
            className="h-full w-full"
            zoomControl={false}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <DraggableMarker
              position={selectedPosition}
              onPositionChange={handlePositionChange}
            />
            <MapClickHandler onMapClick={handlePositionChange} />
            <RecenterButton position={selectedPosition} />
          </MapContainer>

          <button
            onClick={handleGetCurrentLocation}
            className="absolute top-4 right-4 z-[1000] bg-white px-4 py-2 rounded-full shadow-lg hover:bg-gray-50 transition-colors flex items-center gap-2 text-sm font-medium text-gray-700"
          >
            <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Mi ubicación
          </button>
        </div>

        <div className="p-4 bg-gray-50 border-t">
          <div className="flex items-start gap-3 mb-4">
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
              <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900">Ubicación seleccionada</p>
              {isLoadingAddress ? (
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                  Buscando dirección...
                </div>
              ) : (
                <p className="text-sm text-gray-600 truncate">{address}</p>
              )}
              <p className="text-xs text-gray-400 mt-1">
                {selectedPosition[0].toFixed(6)}, {selectedPosition[1].toFixed(6)}
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="flex-1 px-4 py-3 bg-gray-200 text-gray-700 rounded-xl font-medium hover:bg-gray-300 transition-colors"
            >
              Cancelar
            </button>
            <button
              onClick={handleConfirm}
              className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Confirmar ubicación
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LocationPickerMap;
