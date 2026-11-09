package androidx.media3.exoplayer.trackselection;

import android.content.Context;

import androidx.annotation.NonNull;

/**
 * Stand-in for the dual subtitle track selector that FongMi/media does not publish.
 *
 * <p>The real one selects tracks for a second, libass-rendered subtitle view. This one
 * selects nothing extra and delegates every call to the factory it wraps, which keeps
 * video, audio and primary subtitle selection behaving exactly as before.
 */
@SuppressWarnings("unused")
public final class SecondaryTextTrackSelector {

    private SecondaryTextTrackSelector() {
    }

    /** Delegates to the wrapped factory; the second subtitle track is simply not offered. */
    public static final class Factory implements TrackSelector.Factory {

        private final TrackSelector.Factory delegate;

        public Factory(TrackSelector.Factory delegate) {
            if (delegate == null) throw new NullPointerException("delegate");
            this.delegate = delegate;
        }

        @NonNull
        @Override
        public TrackSelector createTrackSelector(@NonNull Context context) {
            return delegate.createTrackSelector(context);
        }
    }
}
