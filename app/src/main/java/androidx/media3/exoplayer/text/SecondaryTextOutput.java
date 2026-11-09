package androidx.media3.exoplayer.text;

import androidx.media3.common.text.CueGroup;

/**
 * Stand-in for the second subtitle output that FongMi/media does not publish.
 *
 * <p>ExoRenderersFactory adds a TextRenderer over this unconditionally, so cues really do
 * arrive here. They are discarded on purpose: with libass unavailable there is no second
 * subtitle view to draw into, and discarding cannot affect the primary renderer, which
 * still receives its own separate output.
 */
public final class SecondaryTextOutput implements TextOutput {

    @Override
    public void onCues(CueGroup cueGroup) {
    }
}
