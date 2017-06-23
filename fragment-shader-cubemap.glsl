#version 320 es
#define M_PI 3.141592653589

precision highp float;
out vec4 outputColor;
in vec2 texCoordOut;
uniform vec4 quaternion;
uniform sampler2D BaseImage;

vec2 flatToSpherical(vec3 flatCoord, float r)
{
  return vec2(
      atan(flatCoord.y, flatCoord.x),
      acos(flatCoord.z / r));
}

mat3 constructCompleteRotation(vec3 a)
{
  return mat3(
      cos(a.x) * cos(a.z) - sin(a.x) * cos(a.y) * sin(a.z),
      -cos(a.x) * sin(a.z) - sin(a.x) * cos(a.y) * cos(a.z),
      sin(a.x) * sin(a.y),
      sin(a.x) * cos(a.z) + cos(a.x) * cos(a.y) * sin(a.z),
      -sin(a.x) * sin(a.z) + cos(a.x) * cos(a.y) * cos(a.z),
      -cos(a.x) * sin(a.y),
      sin(a.y) * sin(a.z),
      sin(a.y) * cos(a.z),
      cos(a.y)
      );
}

int get_face(vec2 uv){
  int x = int(floor(uv.x * 3.0));
  int y = 1 - int(floor(uv.y * 2.0));
  return y * 3 + x;
}

void main() {
  vec2 uv = texCoordOut;
  vec2 faceCoord = uv * 2.0 - 1.0;
  int face = get_face(uv);
  vec3 latSphereCoord;
  vec3 rot;

  if(face == 0){
    rot = vec3(-M_PI / 2.0, 0, 0);
  }else if(face == 1){
    rot = vec3(M_PI / 2.0, 0, 0);
  }else if(face == 2){
    rot = vec3(M_PI / 2.0, M_PI / 2.0, M_PI / 2.0);
  }else if(face == 3){
    rot = vec3(M_PI / 2.0, -M_PI / 2.0, M_PI / 2.0);
  }else if(face == 4){
    rot = vec3(M_PI, 0, 0);
  }else if(face == 5){
    rot = vec3(0, 0, 0);
  }

  latSphereCoord = vec3(1.0,
                        faceCoord.x * 3.0 + 2.0 - float(face % 3) * 2.0,
                        faceCoord.y * 2.0 - 1.0 + float(face / 3) * 2.0);

  float r = sqrt(latSphereCoord.x * latSphereCoord.x +
                latSphereCoord.y * latSphereCoord.y +
                latSphereCoord.z * latSphereCoord.z);

  vec3 rotatedCoord = latSphereCoord * constructCompleteRotation(rot);
  vec2 invRotatedSphericalCoord = flatToSpherical(rotatedCoord, r);

  vec2 finalCoordenates;
  finalCoordenates.x = (invRotatedSphericalCoord.x) / (2.0 * M_PI);
  finalCoordenates.y = (invRotatedSphericalCoord.y) / (M_PI);

  outputColor = texture(BaseImage, mod(finalCoordenates, 1.0));
}
