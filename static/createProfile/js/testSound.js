var mic, recorder, soundFile;

/**
 * States needed:
 * 0 Starting state, wait till first sound > threshold
 * 1 No sound, increment timeSilent, wait till timeSilent > noSoundTime
 * 2 Send sound file, go back to 0
 */

var state = 0; // mousePress will increment from Record, to Stop, to Play
var timeSilent = 0;
var noSoundTime = 100;
var micThreshold = .2; // Laptop .01, phone .002
function setup() {
  createCanvas(400,400);
  // create an audio in
  mic = new p5.AudioIn();

  // users must manually enable their browser microphone for recording to work properly!
  mic.start();

  // create a sound recorder
  recorder = new p5.SoundRecorder();

  // connect the mic to the recorder
  recorder.setInput(mic);

  // create an empty sound file that we will use to playback the recording
  soundFile = new p5.SoundFile();
}

function draw() {
  // fill(0);
  // background(200);
  micLevel = mic.getLevel();
  // text('Mic volume: ' + str(micLevel), 20, 40);

  // if (micLevel > micThreshold) {
  //   fill(0,255,0);
  // }
  // rect(20,60,50,50);
  if (state == 0) {
    // fill(0);
    // text('Just started. Speak to start recording.', 20, 20);
    if (micLevel > micThreshold) {
      recorder.record(soundFile);
      state += 1;
    }
  }
  else if (state == 1) {
    // fill(0);
    // text('Recording!', 20, 20);
    // fill(255,0,0);

    if (timeSilent > noSoundTime) {
      state += 1;
      timeSilent = 0;
      // fill(0,255,0);
    }
    // ellipse(200,100,50,50);
    if (micLevel < micThreshold) {
      timeSilent += 1;
    }
    if (micLevel >micThreshold) {
      timeSilent = 0;
    }
  }
  else if (state == 2) {
    // fill(0);
    // text('Sending!', 20, 20);
    // fill(0,255,0);
    // ellipse(200,100,50,50);
    recorder.stop();
    var fileName = 'mySound.wav';
    postFile(soundFile, fileName);
    soundFile = new p5.SoundFile();
    // state = (state + 1) % 3;
    recorder.record(soundFile);
    state = 1;
  }
}

// function touchStarted() {
//   // use the '.enabled' boolean to make sure user enabled the mic (otherwise we'd record silence)
//   if (state === 0 && mic.enabled) {
//     // Tell recorder to record to a p5.SoundFile which we will use for playback
//     recorder.record(soundFile);
//   }

//   else if (state === 1) {
//     recorder.stop(); // stop recorder, and send the result to soundFile
//   }

//   else if (state === 2) {
//     soundFile.play(); // play the result!
//     var fileName = 'mySound.wav';
//     postFile(soundFile, fileName);
//   }
// }


async function postFile(wavFile, name) {
  postUrl = 'getKeywords/';
  fieldName = 'data';
  filePath = wavFile;
  data = mySaveSound(wavFile, name);
  var blob = new Blob([data], {'type': 'application/octet-stream'});
  var fileOfBlob = new File([blob], 'wei.wav');
  upload(postUrl, fileOfBlob);
}

function upload(postUrl, file) {
  var formData = new FormData();
  formData.append("filee", file);

  $.ajax({
    type: 'POST',
    url: postUrl,
    data: formData,
    processData: false,
    contentType: false
  }).done(function(data) {
       $("#keywords").text(data);
  });
}

/**
 *  Save a p5.SoundFile as a .wav audio file.
 *
 *  @method saveSound
 *  @param  {p5.SoundFile} soundFile p5.SoundFile that you wish to save
 *  @param  {String} name      name of the resulting .wav file.
 */
function mySaveSound(soundFile, name) {
  // helper methods to save waves
  function interleave(leftChannel, rightChannel) {
    var length = leftChannel.length + rightChannel.length;
    var result = new Float32Array(length);
    var inputIndex = 0;
    for (var index = 0; index < length;) {
      result[index++] = leftChannel[inputIndex];
      result[index++] = rightChannel[inputIndex];
      inputIndex++;
    }
    return result;
  }
  function writeUTFBytes(view, offset, string) {
    var lng = string.length;
    for (var i = 0; i < lng; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  }

  var leftChannel, rightChannel;
  leftChannel = soundFile.buffer.getChannelData(0);
  // handle mono files
  if (soundFile.buffer.numberOfChannels > 1) {
    console.log('multichannel');
    rightChannel = soundFile.buffer.getChannelData(1);
  } else {
    rightChannel = leftChannel;
  }
  // var interleaved = interleave(leftChannel, rightChannel);
  var interleaved = leftChannel;
  // create the buffer and view to create the .WAV file
  var buffer = new window.ArrayBuffer(44 + interleaved.length * 2);
  var view = new window.DataView(buffer);
  // write the WAV container,
  // check spec at: https://ccrma.stanford.edu/courses/422/projects/WaveFormat/
  // RIFF chunk descriptor
  writeUTFBytes(view, 0, 'RIFF');
  view.setUint32(4, 36 + interleaved.length * 2, true);
  writeUTFBytes(view, 8, 'WAVE');
  // FMT sub-chunk
  writeUTFBytes(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  // stereo (2 channels)
  view.setUint16(22, 1, true); // # channels
  view.setUint32(24, 44100, true);
  // view.setUint32(28, 44100 * 4, true);
  view.setUint32(28, 44100 * 2, true);
  view.setUint16(32, 4, true);
  view.setUint16(34, 16, true);
  // data sub-chunk
  writeUTFBytes(view, 36, 'data');
  view.setUint32(40, interleaved.length * 2, true);
  view.setUint32(40, interleaved.length, true);
  // write the PCM samples
  var lng = interleaved.length;
  var index = 44;
  var volume = 1;
  for (var i = 0; i < lng; i++) {
    view.setInt16(index, interleaved[i] * (32767 * volume), true);
    index += 2;
  }
  // p5.prototype.writeFile([view], name, 'wav');
  return view;
};
