test -f edubot-snap.zip && rm edubot-snap.zip
cd app
zip -r ../edubot-snap.zip *
cd ..
echo '#!/usr/bin/env python' | cat - edubot-snap.zip > edubot-snap
chmod +x edubot-snap

